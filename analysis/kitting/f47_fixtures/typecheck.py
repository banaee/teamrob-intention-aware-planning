#!/usr/bin/env python3
"""typecheck.py — applies shared.types.check_task_bindings to every registered kitting fixture (every agent's
scheduled and assigned tasks against its layout's objects), and to the retired scenario_60/61 against
env_layout6.json. Prints one line per fixture: PASS, or FAIL with the first error. No simulator run."""
import sys, os, json, importlib.util
from pathlib import Path
sys.path.insert(0, os.getcwd())
from shared.types import check_task_bindings
from domains.kitting.registry import domain_config
HERE = Path(__file__).parent
def types_of(layout_path):
    return {o['id']: o['type'] for o in json.load(open(layout_path))['env_objects']}
def check(sc, layout_path):
    t = types_of(layout_path)
    for a in sc.agents:
        for task in list(a.scheduled_tasks or []) + list(a.assigned_tasks or []):
            try: check_task_bindings(task, t)
            except ValueError as e: return f"FAIL  ({a.agent_id}) {e}"
    return "PASS"
for lay, cfg in domain_config['layouts'].items():
    for sid, sc in cfg['scenarios'].items():
        print(f"{sid:12s} {lay:12s} {check(sc, cfg['path'])}")
spec = importlib.util.spec_from_file_location("retired", HERE / "retired_scenarios_60_61.py")
retired = importlib.util.module_from_spec(spec); spec.loader.exec_module(retired)
for sc in (retired.scenario_60, retired.scenario_61):
    print(f"{sc.id:12s} {'env_layout6':12s} {check(sc, 'domains/kitting/env_layout6.json')}  [retired]")
