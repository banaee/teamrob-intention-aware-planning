"""
webui/

The web-ui (T-viz): its message definitions (messages.py), the interface a simulator's piece implements (simulator.py),
the scene appearance's definitions (appearance.py), the JSON Schema the page's types are generated from (schema.py),
and the page (page/; since 0.3 the env-pane, drawn from saved messages); its server comes later. Independent of every
simulator and every domain: nothing here imports mesa_sim/, domains/, shared/ or world/, and neither the Python nor the
page names a domain, an object type or an area id (tests/test_tviz_messages.py). A simulator supplies its own piece,
which imports from here (Mesa's: mesa_sim/webui_adapter.py).
"""
