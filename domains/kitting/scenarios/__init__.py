# domains/kitting/scenarios/__init__.py
"""
The kitting scenarios package (T-L stage 2): one module per setup,
scenarios_sNN.py holding every scenario whose setup is env_setup_NN and no
other. The serial in a module's name repeats its scenarios' validated `setup`
field — an authoring convention the code does not check, as the serial in a
scenario id is (T-L, ruling 4). Scenarios are registered by discovery
(domains/discovery.py) at import of domains.kitting.registry: no hand-written
list, and a duplicate id is an error at import.
"""
