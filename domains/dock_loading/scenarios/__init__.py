# domains/dock_loading/scenarios/__init__.py
"""
The dock_loading scenarios package (T-L stage 2): one module per setup,
scenarios_sNN.py holding every scenario whose setup is env_setup_NN and no
other — an authoring convention the code does not check, as in kitting.
Scenarios are registered by discovery (domains/discovery.py) at import of
domains.dock_loading.registry: no hand-written list, and a duplicate id is an
error at import.
"""
