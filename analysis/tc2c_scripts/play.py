"""analysis/tc2c_scripts/play.py <scenario_9N> [run_mesa flags...] — T-C2c play: six scratch scenarios, injected into the kitting
registry in memory (not registered in the repo), then the normal headless run. Run from the repo root."""
import sys
sys.path.insert(0, ".")
from shared.types import Var, Const, TaskInstance, AgentConfig, ScenarioConfig
from domains.kitting.tasks import deliver_item, coffee_break
from domains.kitting.scenarios import scenario_00, scenario_10, scenario_80
from domains.kitting.script import MoveTo, Stay, interrupt, deviate, abandon
from domains.kitting.registry import domain_config

def d(item, table):
    return TaskInstance(schema=deliver_item, bindings={Var("?item"): Const(item), Var("?kitting_table"): Const(table)})
coffee = TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})

def variant(base, sid, script, assigned):
    human = next(a for a in base.agents if a.agent_type == "human")
    robot = next(a for a in base.agents if a.agent_type == "robot")
    h = AgentConfig(agent_id=human.agent_id, agent_type="human", start_position=human.start_position,
                    scheduled_tasks=script, assigned_tasks=assigned, observes=[])
    return ScenarioConfig(id=sid, name=sid, description="T-C2c play (scratch)", agents=[h, robot])

K0, K1 = "kitting_table_0", "kitting_table_1"
PLAY = {
    "scenario_91": ("env_layout8", variant(scenario_80, "scenario_91",
        [*abandon(d("item_3", K1), before="pick_up"), d("item_0", K0)], [d("item_0", K0), d("item_3", K1)])),
    "scenario_92": ("env_layout0", variant(scenario_00, "scenario_92",
        [*abandon(d("item_3", K0), after="pick_up", then=[d("item_2", K0)])], [d("item_3", K0), d("item_2", K0)])),
    "scenario_93": ("env_layout8", variant(scenario_80, "scenario_93",
        [*deviate(d("item_0", K0), destination=K1), d("item_3", K1)], [d("item_0", K0), d("item_3", K1)])),
    "scenario_94": ("env_layout0", variant(scenario_00, "scenario_94",
        [*interrupt(d("item_3", K0), after="pick_up", with_=[MoveTo("corner_NE"), Stay(30)]), d("item_2", K0)],
        [d("item_3", K0), d("item_2", K0)])),
    "scenario_95": ("env_layout1", variant(scenario_10, "scenario_95",
        [*interrupt(d("item_2", K0), after="pick_up", with_=[coffee]), Stay(20),
         *abandon(d("item_5", K0), after="pick_up")], [d("item_2", K0), d("item_5", K0)])),
    "scenario_96": ("env_layout0", variant(scenario_00, "scenario_96",
        [MoveTo("door"), Stay(20), MoveTo("corner_SW"), d("item_3", K0)], [d("item_3", K0)])),
}
for sid, (layout, sc) in PLAY.items():
    domain_config["layouts"][layout]["scenarios"][sid] = sc

sid = sys.argv[1]
sys.argv = ["run_mesa.py", "--domain", "kitting", "--layout", PLAY[sid][0], "--scenario", sid] + sys.argv[2:]
from mesa_sim.run_mesa import run_headless
run_headless()
