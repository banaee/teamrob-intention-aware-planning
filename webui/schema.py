"""
webui/schema.py

PURPOSE:
    Writes the JSON Schema of what the page reads (the messages of webui/messages.py and the scene appearance of
    webui/appearance.py) to webui/page/src/gen/messages.schema.json; the page's TypeScript types are generated from it
    (webui/page: `npm run gen:types`). The Python definitions are the one source; the generated files are committed so
    the page builds without Python.

    ~/python-envs/ir-nomesa-env/bin/python -m webui.schema
"""

import json
from pathlib import Path

from pydantic.json_schema import models_json_schema

from webui.appearance import Appearance
from webui.messages import Catalogue, RunDescription, SimRunChoice, TickUpdate

OUT = Path(__file__).parent / "page" / "src" / "gen" / "messages.schema.json"
PAGE_TYPES = (Catalogue, SimRunChoice, RunDescription, TickUpdate, Appearance)


def _for_the_page(schema: dict) -> dict:
    """The schema of the JSON the page reads: every field present (a message is written with all its fields, defaults
    included), and no property title or default, so the generated types are named by their classes alone."""
    for definition in schema["$defs"].values():
        properties = definition.get("properties")
        if properties is not None:
            definition["required"] = sorted(properties)
            for prop in properties.values():
                prop.pop("title", None)
                prop.pop("default", None)
    return schema


def main() -> None:
    _, schema = models_json_schema([(t, "serialization") for t in PAGE_TYPES], title="WebUiMessages")
    schema = _for_the_page(schema)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    print("[webui.schema] wrote", OUT)


if __name__ == "__main__":
    main()
