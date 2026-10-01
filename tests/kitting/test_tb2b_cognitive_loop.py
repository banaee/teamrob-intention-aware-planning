"""
TB.2b: the cognitive loop does not end with the task pool (design_decisions.md, the entry of that name).

Observation and recognition run on every tick; an empty task pool stops planning and execution only: after the
terminal return no trigger is evaluated, nothing is decided and the executor is not stepped. Two cases, on
registered scenarios with the prior on: the robot's pool replaced by an empty one (empty from tick 0), and the
scenario as registered (the pool empties mid-run).
"""
import logging
import re
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mesa_sim"))

from domains.kitting.registry import domain_config, register_kitting_domain
from mesa_sim.sim_model import SimModel

STEP = re.compile(r"step=(\d+)")
DONE = re.compile(r"^\[meta\] step=(\d+) all tasks complete$")


def model_for(layout, sid, empty_pool=False):
    """The registered scenario, prior on; with `empty_pool` the robot's assigned_tasks replaced by none."""
    scenario = domain_config["scenarios"][sid]
    if empty_pool:
        scenario = replace(scenario, agents=[replace(a, assigned_tasks=[]) if a.agent_type == "robot" else a
                                             for a in scenario.agents])
    return SimModel(scenario=scenario, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"][layout],
                    setup_path=domain_config["setups"][scenario.setup],
                    assignment_prior=True)


def run_lines(m, steps, caplog):
    with caplog.at_level(logging.INFO):
        for _ in range(steps):
            m.step()
    return [r.getMessage() for r in caplog.records]


def steps_of(lines, prefix):
    return [int(STEP.search(l)[1]) for l in lines if l.startswith(prefix)]


def test_an_empty_pool_observes_every_tick_and_completes_once_at_tick_0(caplog):
    m = model_for("env_layout_01", "scenario_s01_01", empty_pool=True)
    robot = next(iter(m.observing))
    robot_agent = next(a for a in m.schedule.agents if a.unique_id == robot)
    start = robot_agent.pos
    steps = 60
    lines = run_lines(m, steps, caplog)
    assert steps_of(lines, "[IR] step=") == list(range(steps))
    assert steps_of(lines, "[IR-dist] step=") == list(range(steps))
    assert [int(DONE.match(l)[1]) for l in lines if DONE.match(l)] == [0]
    assert steps_of(lines, "[meta-trig] step=") == [0]
    assert robot_agent.pos == start


def test_a_pool_that_empties_mid_run_keeps_observing_and_evaluates_no_trigger(caplog):
    # scenario_s03_06 (scenario_s03_01's end-state variant: the human's script ends away from the robot's table), not
    # scenario_s01_06 as before T-D P: under P that pool never empties (the robot waits, occupied target, X)
    steps = 300
    lines = run_lines(model_for("env_layout_06", "scenario_s03_06"), steps, caplog)
    done = [int(DONE.match(l)[1]) for l in lines if DONE.match(l)]
    assert len(done) == 1 and done[0] < steps - 1
    d = done[0]
    assert steps_of(lines, "[IR] step=") == list(range(steps))
    assert [t for t in steps_of(lines, "[IR] step=") if t > d] == list(range(d + 1, steps))
    assert not [t for t in steps_of(lines, "[meta-trig] step=") if t > d]
    after = lines[next(i for i, l in enumerate(lines) if DONE.match(l)) + 1:]
    assert not [l for l in after if l.startswith("[meta")]
