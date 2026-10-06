"""
webui/

The web-ui (T-viz): its message definitions (messages.py) and the interface a simulator's piece implements
(simulator.py); its server and its page come later. Independent of every simulator and every domain: nothing here
imports mesa_sim/, domains/, shared/ or world/ (tests/test_tviz_messages.py). A simulator supplies its own piece, which
imports from here (Mesa's: mesa_sim/webui_adapter.py).
"""
