"""
control_run.py — the F47 control, kept for the record: the RETIRED env_layout6 (domains/kitting/env_layout6.json,
unregistered) with its waypoint wander_0 retyped as a coffee machine and the retired scenario_60 / _61's first
human task bound to it, so the stay is MODELLED. Measured (F47): no [stop] at all — at the crossing (tick 23)
B3 switches to the alternative in the beside variant (item_2 80.15 vs item_1 + hold 32 = 89, done 185) and holds
32 ticks in the across variant (done 204 / 209). Registers the scratch layout in the kitting registry in-process
and runs run_mesa headless with the usual flags:
    PYTHONHASHSEED=0 python analysis/f47_fixtures/control_run.py --domain kitting --layout env_layout6c \\
        --scenario scenario_60c --steps 300 --assignment_prior false --cost_strategy realized \\
        --gate_strategy none --separation_stop true
Note: scenario_60/61's other two human tasks (coffee_break(wander_1), an ill-typed binding) are left as they
were; the spawn type check (F47b) refuses them, so this control can no longer run unmodified — it is the
record of what was measured, not a live fixture.
"""
import sys, os, json, copy, importlib.util
from pathlib import Path
sys.path.insert(0, os.getcwd())
HERE = Path(__file__).parent
SCRATCH = Path(os.environ.get("F47_SCRATCH", HERE / "_scratch")); SCRATCH.mkdir(exist_ok=True)
l6 = json.load(open('domains/kitting/env_layout6.json'))
for o in l6['env_objects']:
    if o['id'] == 'wander_0':
        o['id'] = 'coffee_machine_0'; o['type'] = 'coffee_machine'; o['size'] = [50, 50]
json.dump(l6, open(SCRATCH / 'env_layout6c.json', 'w'))
from shared.types import TaskInstance, Var, Const
from domains.kitting.registry import domain_config
from domains.kitting.tasks import coffee_break
spec = importlib.util.spec_from_file_location("retired", HERE / "retired_scenarios_60_61.py")
retired = importlib.util.module_from_spec(spec); spec.loader.exec_module(retired)
def ctl(sc, sid):
    c = copy.deepcopy(sc); c.id = sid
    c.agents[0].scheduled_tasks[0] = TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})
    return c
domain_config['layouts']['env_layout6c'] = {'path': str(SCRATCH / 'env_layout6c.json'),
    'scenarios': {'scenario_60c': ctl(retired.scenario_60, 'scenario_60c'), 'scenario_61c': ctl(retired.scenario_61, 'scenario_61c')}}
from mesa_sim import run_mesa
run_mesa.run_headless()
